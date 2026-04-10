package com.nageoffer.ai.tender.config.response;

import java.util.Objects;

/**
 * Represents the standard API response envelope.
 *
 * @param code the machine-readable result code
 * @param message the result message
 * @param data the response payload
 * @param <T> the payload type
 */
public record Response<T>(String code, String message, T data) {

    /**
     * Creates a success response without a payload.
     *
     * @return the success response
     */
    public static Response<Void> success() {
        return new Response<>("OK", "Success", null);
    }

    /**
     * Creates a success response with a payload.
     *
     * @param data the response payload
     * @return the success response
     * @param <T> the payload type
     */
    public static <T> Response<T> success(T data) {
        return new Response<>("OK", "Success", data);
    }

    /**
     * Creates a failure response from a code-message pair.
     *
     * @param code the error code
     * @param message the error message
     * @return the failure response
     * @param <T> the payload type
     */
    public static <T> Response<T> failure(String code, String message) {
        return new Response<>(Objects.requireNonNull(code, "code must not be null"),
            Objects.requireNonNull(message, "message must not be null"), null);
    }
}
